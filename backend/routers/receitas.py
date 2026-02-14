from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from database import get_supabase_client

router = APIRouter()


@router.get("/test-tables")
async def test_receitas_table():
    """
    Testa se a tabela Receita existe e retorna informações sobre ela
    """
    supabase = get_supabase_client()
    results = {}
    
    try:
        # Teste 1: Select normal
        response1 = supabase.table("Receita").select("*").execute()
        
        # Teste 2: Select com count
        response2 = supabase.table("Receita").select("*", count="exact").execute()
        
        results["Receita"] = {
            "select_all": {
                "success": True,
                "data_count": len(response1.data) if response1.data else 0,
                "has_data": bool(response1.data),
                "sample_data": response1.data[:2] if response1.data else []
            },
            "with_count": {
                "count": response2.count if hasattr(response2, 'count') else "N/A",
                "data_count": len(response2.data) if response2.data else 0
            }
        }
    except Exception as e:
        results["Receita"] = {
            "success": False,
            "error": str(e)
        }
    
    return results


@router.get("")
async def get_receitas():
    """
    Retorna todas as receitas com suas informações completas incluindo calorias totais
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("Receita").select("*").execute()
        receitas = response.data or []
        
        # Para cada receita, buscar as calorias totais
        receitas_com_calorias = []
        for receita in receitas:
            receita_id = receita.get("id")
            
            try:
                # Buscar ingredientes desta receita
                ingredients_response = supabase.table("ReceitaIngrediente").select("*").eq("idReceita", receita_id).execute()
                recipe_ingredients = ingredients_response.data or []
                
                # Calcular total de calorias
                total_calorias = 0
                for rec_ing in recipe_ingredients:
                    ingredient_id = rec_ing.get("idIngrediente")
                    quantidade = rec_ing.get("quantidade", 0)
                    
                    try:
                        # Buscar ingrediente completo
                        ing_response = supabase.table("Ingrediente").select("*").eq("id", ingredient_id).single().execute()
                        ingredient = ing_response.data
                        
                        if ingredient:
                            calorias_por_unidade = (ingredient.get("calorias") or ingredient.get("calories") or 0) / 100
                            total_calorias += quantidade * calorias_por_unidade
                    except:
                        # Se falhar ao buscar ingrediente, continua
                        pass
                
                # Adicionar calorias totais à receita
                receita["calorias_totais"] = total_calorias
            except:
                # Se falhar ao buscar ingredientes, deixa sem calorias
                receita["calorias_totais"] = 0
            
            receitas_com_calorias.append(receita)
        
        return receitas_com_calorias
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar receitas: {str(e)}"
        )


@router.get("/minhas")
async def get_minhas_receitas(user_email: str = None):
    """
    Retorna receitas favoritas do usuário com calorias totais
    Usa ReceitaUtilizador (email, idReceita) filtrando por favorita=true
    """
    try:
        supabase = get_supabase_client()

        if not user_email:
            # Sem usuario, retorna todas as receitas
            response = supabase.table("Receita").select("*").execute()
            receitas = response.data or []

            receitas_com_calorias = []
            for receita in receitas:
                receita_id = receita.get("id")

                try:
                    ingredients_response = (
                        supabase.table("ReceitaIngrediente")
                        .select("*")
                        .eq("idReceita", receita_id)
                        .execute()
                    )
                    recipe_ingredients = ingredients_response.data or []

                    total_calorias = 0
                    for rec_ing in recipe_ingredients:
                        ingredient_id = rec_ing.get("idIngrediente")
                        quantidade = rec_ing.get("quantidade", 0)

                        try:
                            ing_response = (
                                supabase.table("Ingrediente")
                                .select("*")
                                .eq("id", ingredient_id)
                                .single()
                                .execute()
                            )
                            ingredient = ing_response.data

                            if ingredient:
                                calorias_por_unidade = (ingredient.get("calorias") or ingredient.get("calories") or 0) / 100
                                total_calorias += quantidade * calorias_por_unidade
                        except Exception:
                            pass

                    receita["calorias_totais"] = total_calorias
                except Exception:
                    receita["calorias_totais"] = 0

                receitas_com_calorias.append(receita)

            return receitas_com_calorias

        # Buscar receitas favoritas do usuario
        # NOTA: ReceitaUtilizador pode não ter dados ainda. Se não houver, retorna vazio
        try:
            rel_response = (
                supabase.table("ReceitaUtilizador")
                .select("idReceita")
                .eq("idUtilizador", user_email)  # Usando idUtilizador em vez de email
                .eq("favorita", True)
                .execute()
            )
            receita_ids = [r.get("idReceita") for r in (rel_response.data or []) if r.get("idReceita") is not None]
        except Exception as e:
            # Se a tabela não existe ou tem erro, retorna vazio (não há receitas favoritas ainda)
            print(f"Erro ao buscar ReceitaUtilizador: {str(e)}")
            return []
        
        if not receita_ids:
            return []

        response = supabase.table("Receita").select("*").in_("id", receita_ids).execute()
        receitas = response.data or []

        # Calcular calorias para cada receita
        receitas_com_calorias = []
        for receita in receitas:
            receita_id = receita.get("id")

            try:
                # Buscar ingredientes desta receita
                ingredients_response = (
                    supabase.table("ReceitaIngrediente")
                    .select("*")
                    .eq("idReceita", receita_id)
                    .execute()
                )
                recipe_ingredients = ingredients_response.data or []

                # Calcular total de calorias
                total_calorias = 0
                for rec_ing in recipe_ingredients:
                    ingredient_id = rec_ing.get("idIngrediente")
                    quantidade = rec_ing.get("quantidade", 0)

                    try:
                        # Buscar ingrediente completo
                        ing_response = (
                            supabase.table("Ingrediente")
                            .select("*")
                            .eq("id", ingredient_id)
                            .single()
                            .execute()
                        )
                        ingredient = ing_response.data

                        if ingredient:
                            calorias_por_unidade = (ingredient.get("calorias") or ingredient.get("calories") or 0) / 100
                            total_calorias += quantidade * calorias_por_unidade
                    except Exception:
                        pass

                receita["calorias_totais"] = total_calorias
            except Exception:
                receita["calorias_totais"] = 0

            receitas_com_calorias.append(receita)

        return receitas_com_calorias

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar minhas receitas: {str(e)}"
        )




@router.get("/outras")
async def get_outras_receitas(user_email: str = None):
    """
    Retorna receitas nao favoritas do usuario e receitas sem relacao com o usuario
    Usa ReceitaUtilizador (email, idReceita) filtrando por favorita=false
    """
    try:
        if not user_email:
            # Se não tem email, retorna todas as receitas
            response = supabase.table("Receita").select("*").execute()
            receitas = response.data or []

            receitas_com_calorias = []
            for receita in receitas:
                receita_id = receita.get("id")

                try:
                    ingredients_response = (
                        supabase.table("ReceitaIngrediente")
                        .select("*")
                        .eq("idReceita", receita_id)
                        .execute()
                    )
                    recipe_ingredients = ingredients_response.data or []

                    total_calorias = 0
                    for rec_ing in recipe_ingredients:
                        ingredient_id = rec_ing.get("idIngrediente")
                        quantidade = rec_ing.get("quantidade", 0)

                        try:
                            ing_response = (
                                supabase.table("Ingrediente")
                                .select("*")
                                .eq("id", ingredient_id)
                                .single()
                                .execute()
                            )
                            ingredient = ing_response.data

                            if ingredient:
                                calorias_por_unidade = (ingredient.get("calorias") or ingredient.get("calories") or 0) / 100
                                total_calorias += quantidade * calorias_por_unidade
                        except Exception:
                            pass

                    receita["calorias_totais"] = total_calorias
                except Exception:
                    receita["calorias_totais"] = 0

                receitas_com_calorias.append(receita)

            return receitas_com_calorias

        supabase = get_supabase_client()

        # Buscar receitas nao favoritas do usuario
        # NOTA: ReceitaUtilizador pode não ter dados ainda. Se não houver, retorna todas as receitas
        try:
            rel_response = (
                supabase.table("ReceitaUtilizador")
                .select("idReceita")
                .eq("idUtilizador", user_email)
                .eq("favorita", False)
                .execute()
            )

            # Buscar todas as relacoes do usuario para excluir do "sem relacao"
            user_rel_response = (
                supabase.table("ReceitaUtilizador")
                .select("idReceita")
                .eq("idUtilizador", user_email)
                .execute()
            )

            nao_favoritas_ids = {
                r.get("idReceita")
                for r in (rel_response.data or [])
                if r.get("idReceita") is not None
            }
            user_rel_ids = {
                r.get("idReceita")
                for r in (user_rel_response.data or [])
                if r.get("idReceita") is not None
            }
        except Exception as e:
            # Se a tabela não existe ou tem erro, considera que não há relações
            print(f"Erro ao buscar ReceitaUtilizador: {str(e)}")
            nao_favoritas_ids = set()
            user_rel_ids = set()

        # Buscar receitas sem relacao com o usuario
        all_recipes_response = supabase.table("Receita").select("id").execute()
        all_recipe_ids = {
            r.get("id")
            for r in (all_recipes_response.data or [])
            if r.get("id") is not None
        }
        sem_relacao_ids = all_recipe_ids - user_rel_ids

        receita_ids = list(nao_favoritas_ids | sem_relacao_ids)
        if not receita_ids:
            return []

        response = supabase.table("Receita").select("*").in_("id", receita_ids).execute()
        receitas = response.data or []

        # Calcular calorias para cada receita
        receitas_com_calorias = []
        for receita in receitas:
            receita_id = receita.get("id")

            try:
                # Buscar ingredientes desta receita
                ingredients_response = (
                    supabase.table("ReceitaIngrediente")
                    .select("*")
                    .eq("idReceita", receita_id)
                    .execute()
                )
                recipe_ingredients = ingredients_response.data or []

                # Calcular total de calorias
                total_calorias = 0
                for rec_ing in recipe_ingredients:
                    ingredient_id = rec_ing.get("idIngrediente")
                    quantidade = rec_ing.get("quantidade", 0)

                    try:
                        # Buscar ingrediente completo
                        ing_response = (
                            supabase.table("Ingrediente")
                            .select("*")
                            .eq("id", ingredient_id)
                            .single()
                            .execute()
                        )
                        ingredient = ing_response.data

                        if ingredient:
                            calorias_por_unidade = (ingredient.get("calorias") or ingredient.get("calories") or 0) / 100
                            total_calorias += quantidade * calorias_por_unidade
                    except Exception:
                        pass

                receita["calorias_totais"] = total_calorias
            except Exception:
                receita["calorias_totais"] = 0

            receitas_com_calorias.append(receita)

        return receitas_com_calorias

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar outras receitas: {str(e)}"
        )


@router.get("/{recipe_id}")
async def get_recipe_with_ingredients(recipe_id: int):
    """
    Retorna uma receita com todos seus ingredientes e calorias
    Busca na tabela ReceitaIngrediente os ingredientes e suas quantidades
    E depois busca as calorias de cada ingrediente na tabela Ingrediente
    """
    try:
        supabase = get_supabase_client()
        
        # 1. Buscar a receita
        recipe_response = supabase.table("Receita").select("*").eq("id", recipe_id).single().execute()
        recipe = recipe_response.data
        
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
        
        # 2. Buscar ingredientes desta receita na tabela ReceitaIngrediente
        ingredients_response = supabase.table("ReceitaIngrediente").select("*").eq("idReceita", recipe_id).execute()
        recipe_ingredients = ingredients_response.data or []
        
        # 3. Para cada ingrediente, buscar os detalhes completos na tabela Ingrediente
        ingredients_with_details = []
        for rec_ing in recipe_ingredients:
            ingredient_id = rec_ing.get("idIngrediente")
            quantidade = rec_ing.get("quantidade")
            
            # Buscar ingrediente completo
            ing_response = supabase.table("Ingrediente").select("*").eq("id", ingredient_id).single().execute()
            ingredient = ing_response.data
            
            if ingredient:
                calorias_por_unidade = (ingredient.get("calorias") or ingredient.get("calories") or 0) / 100
                ingredients_with_details.append({
                    "id": ingredient.get("id"),
                    "nome": ingredient.get("nome") or ingredient.get("name"),
                    "quantidade": quantidade,
                    "calorias": calorias_por_unidade,
                    "unidade": rec_ing.get("unidade") or "g"  # g, ml, unidade, etc
                })
        
        # 4. Calcular total de calorias (quantidade * calorias por unidade)
        total_calorias = sum(
            ing.get("quantidade", 0) * ing.get("calorias", 0)
            for ing in ingredients_with_details
        )
        
        # 5. Retornar receita com ingredientes agregados
        return {
            **recipe,
            "ingredientes": ingredients_with_details,
            "calorias_totais": total_calorias,
            "num_ingredientes": len(ingredients_with_details)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar receita com ingredientes: {str(e)}"
        )

