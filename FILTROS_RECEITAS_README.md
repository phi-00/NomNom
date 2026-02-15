# 🔍 Sistema de Filtros para Receitas - Documentação

## 📋 Visão Geral

Sistema completo de filtros para a página "Other Recipes" (`/recipes/otherrecipes`) que permite aos usuários pesquisar receitas com base em múltiplos critérios.

## ✨ Funcionalidades Implementadas

### Filtros Disponíveis

1. **Apenas ingredientes que você tem** ✅
   - Mostra apenas receitas que podem ser feitas com os ingredientes no inventário do usuário
   - Verifica a tabela `Inventário` para comparar com `ReceitaIngrediente`

2. **Nível de Dificuldade** 📊
   - Fácil (enum: `facil`)
   - Médio (enum: `medio`)
   - Difícil (enum: `dificil`)

3. **Categoria** 🍽️
   - Padaria (enum: `padaria`)
   - Pastelaria (enum: `pastelaria`)
   - Entrada (enum: `entrada`)
   - Sopa (enum: `sopa`)
   - Prato Principal (enum: `prato principal`)
   - Bebida (enum: `bebida`)

4. **Tipo de Cozinhado** 🔥
   - Frito (enum: `frito`)
   - Assado (enum: `assado`)
   - Cozido (enum: `cozido`)
   - Grelhado (enum: `grelhado`)
   - Estufado (enum: `estufado`)

5. **Tempo de Preparação** ⏱️
   - Range de minutos (mínimo até máximo)

6. **Número de Porções** 👥
   - Range de porções (mínimo até máximo)

> **Nota Importante:** Os valores dos enums no Supabase são **minúsculos, sem acentos**. Os valores enviados ao backend são: `facil`, `medio`, `dificil`, `padaria`, `pastelaria`, `entrada`, `sopa`, `prato principal`, `bebida`, `frito`, `assado`, `cozido`, `grelhado`, `estufado`. A interface mantém a capitalização apenas para exibição ao usuário.

## 🎨 Interface do Usuário

### Botão de Filtros
- Localizado no topo da página "Other Recipes"
- Abre overlay com formulário de filtros
- Design com gradiente e ícone de lupa 🔍

### Overlay de Filtros
- Painel centralizado com fundo escurecido
- Design moderno e responsivo
- Campos de filtro organizados por categoria
- Botões de ação:
  - **Limpar Filtros**: Remove todos os filtros e recarrega receitas
  - **Aplicar Filtros**: Aplica filtros selecionados e fecha overlay

## 🔧 Arquivos Modificados

### Frontend

#### 1. `NomNom/src/pages/recipes/OtherRecipes.vue`
**Mudanças:**
- ✅ Adicionado botão "Filtros" no header
- ✅ Criado overlay com formulário de filtros
- ✅ Implementada lógica de aplicar/limpar filtros
- ✅ Estilos completos para overlay e painel de filtros

**Novos componentes visuais:**
- `.header-section`: Container do título e botão de filtros
- `.filter-overlay`: Overlay de fundo escurecido
- `.filter-panel`: Painel de filtros centralizado
- `.filter-content`: Área de rolagem com campos de filtro
- `.filter-actions`: Botões de limpar e aplicar

#### 2. `NomNom/src/composables/useRecipes.js`
**Mudanças:**
- ✅ Nova função `fetchOutrasReceitasWithFilters(userEmail, filters)`
- ✅ Constrói parâmetros de query baseados nos filtros ativos
- ✅ Chama endpoint `/api/v1/receitas/outras/filtradas`
- ✅ Exporta nova função no return

**Exemplo de uso:**
```javascript
await fetchOutrasReceitasWithFilters('user@example.com', {
  dificuldade: 'facil',
  categoria: 'entrada',
  tempo_max: 30,
  onlyMyIngredients: true
});
```

### Backend

#### 3. `backend/routers/receitas.py`
**Mudanças:**
- ✅ Novo endpoint `GET /api/v1/receitas/outras/filtradas`
- ✅ Aceita múltiplos parâmetros de query
- ✅ Filtra receitas no Supabase com `.eq()`, `.gte()`, `.lte()`
- ✅ Filtro especial para "apenas meus ingredientes"
- ✅ Exclui receitas favoritas automaticamente
- ✅ Calcula calorias totais para cada receita

**Parâmetros aceitos:**
```python
user_email: str = None
dificuldade: str = None
categoria: str = None
tipo_cozinhado: str = None
tempo_min: int = None
tempo_max: int = None
porcoes_min: int = None
porcoes_max: int = None
only_my_ingredients: bool = False
```

## 🚀 Como Testar

### 1. Iniciar Backend
```powershell
cd c:\Users\felip\OneDrive\Documentos\GitHub\NomNom\backend
python -m uvicorn main:app --reload
```

**Verificar:** Backend rodando em `http://localhost:8000`

### 2. Iniciar Frontend
```powershell
cd c:\Users\felip\OneDrive\Documentos\GitHub\NomNom\NomNom
npm run dev
```

**Verificar:** Frontend rodando em `http://localhost:5173`

### 3. Navegar para Other Recipes
1. Abrir `http://localhost:5173`
2. Ir para `/recipes/otherrecipes` ou clicar em "Other Recipes"

### 4. Testar Filtros

#### Teste 1: Filtro por Dificuldade
1. Clicar no botão "🔍 Filtros"
2. Selecionar "Fácil" em "Nível de Dificuldade"
3. Clicar "Aplicar Filtros"
4. ✅ Deve mostrar apenas receitas fáceis

#### Teste 2: Filtro por Tempo
1. Clicar no botão "🔍 Filtros"
2. Definir tempo máximo = 30 minutos
3. Clicar "Aplicar Filtros"
4. ✅ Deve mostrar apenas receitas até 30 minutos

#### Teste 3: Múltiplos Filtros
1. Clicar no botão "🔍 Filtros"
2. Selecionar:
   - Dificuldade: Fácil (envia `facil`)
   - Categoria: Entrada (envia `entrada`)
   - Tipo de Cozinhado: Assado (envia `assado`)
   - Tempo máximo: 45 minutos
3. Clicar "Aplicar Filtros"
4. ✅ Deve mostrar receitas que atendem TODOS os critérios

#### Teste 4: Apenas Meus Ingredientes
**Pré-requisito:** Usuário deve estar logado e ter ingredientes no inventário

1. Garantir que há dados em `Inventário` para seu usuário
2. Clicar no botão "🔍 Filtros"
3. Marcar "Apenas ingredientes que você tem"
4. Clicar "Aplicar Filtros"
5. ✅ Deve mostrar apenas receitas com todos ingredientes no seu inventário

#### Teste 5: Limpar Filtros
1. Aplicar qualquer filtro
2. Clicar no botão "🔍 Filtros"
3. Clicar "Limpar Filtros"
4. ✅ Deve recarregar todas as receitas (não favoritas)

## 📊 Fluxo de Dados

```
Frontend (OtherRecipes.vue)
    ↓
    1. Usuário clica "Filtros"
    ↓
    2. Overlay abre com formulário
    ↓
    3. Usuário seleciona filtros
    ↓
    4. Clica "Aplicar Filtros"
    ↓
useRecipes.js
    ↓
    5. fetchOutrasReceitasWithFilters() constrói params
    ↓
    6. GET /api/v1/receitas/outras/filtradas
    ↓
Backend (receitas.py)
    ↓
    7. Aplica filtros no Supabase
    ↓
    8. Se only_my_ingredients, verifica Inventário
    ↓
    9. Exclui receitas favoritas
    ↓
    10. Calcula calorias para cada receita
    ↓
    11. Retorna lista filtrada
    ↓
Frontend
    ↓
    12. Atualiza outrasReceitas
    ↓
    13. Fecha overlay
    ↓
    14. Exibe receitas filtradas
```

## 🔍 Endpoints API

### GET `/api/v1/receitas/outras/filtradas`

**Descrição:** Retorna receitas "outras" (não favoritas) com filtros aplicados

**Query Parameters:**
| Parâmetro | Tipo | Obrigatório | Descrição | Valores Aceitos |
|-----------|------|-------------|-----------|-----------------|
| `user_email` | string | Não | Email do usuário | - |
| `dificuldade` | string | Não | Nível de dificuldade | `facil`, `medio`, `dificil` |
| `categoria` | string | Não | Categoria da receita | `padaria`, `pastelaria`, `entrada`, `sopa`, `prato principal`, `bebida` |
| `tipo_cozinhado` | string | Não | Tipo de cozinhado | `frito`, `assado`, `cozido`, `grelhado`, `estufado` |
| `tempo_min` | integer | Não | Tempo mínimo em minutos | Número inteiro positivo |
| `tempo_max` | integer | Não | Tempo máximo em minutos | Número inteiro positivo |
| `porcoes_min` | integer | Não | Porções mínimas | Número inteiro positivo |
| `porcoes_max` | integer | Não | Porções máximas | Número inteiro positivo |
| `only_my_ingredients` | boolean | Não | Filtrar por ingredientes do usuário | `true` ou `false` |

**Exemplo de Request:**
```bash
GET http://localhost:8000/api/v1/receitas/outras/filtradas?user_email=user@example.com&dificuldade=facil&tempo_max=30&only_my_ingredients=true
```

**Exemplo de Response:**
```json
[
  {
    "id": 1,
    "nome": "Salada Simples",
    "descricao": "Uma salada fácil e rápida",
    "tempo_preparacao": 15,
    "num_etapas": 3,
    "porcoes": 2,
    "dificuldade": "facil",
    "categoria": "entrada",
    "tipo_cozinhado": "assado",
    "imagem": "https://...",
    "calorias_totais": 150.5
  }
]
```

## 🎯 Tabelas do Banco de Dados Utilizadas

### Principais
- **Receita**: Dados das receitas
- **ReceitaUtilizador**: Relação usuário-receita (favoritas)
- **ReceitaIngrediente**: Ingredientes de cada receita
- **Ingrediente**: Dados dos ingredientes
- **Inventário**: Ingredientes do usuário

### Schema da Receita
```sql
create table public."Receita" (
  id bigint generated by default as identity not null,
  nome text not null,
  descricao text not null,
  tempo_preparacao integer not null,
  num_etapas integer not null,
  porcoes integer not null,
  dificuldade public.dificuldade not null,
  categoria public.categoria not null,
  tipo_cozinhado public.tipo_cozinhado null,
  imagem text null,
  constraint Receitas_pkey primary key (id)
)
```

## 💡 Dicas de Uso

### Para Desenvolvedores

1. **Adicionar novos filtros:**
   - Adicionar campo no overlay em `OtherRecipes.vue`
   - Adicionar ao objeto `filters` no `ref()`
   - Adicionar ao `activeFilters` em `applyFilters()`
   - Adicionar parâmetro no backend `get_outras_receitas_filtradas()`
   - Adicionar lógica de filtro no Supabase query

2. **Customizar valores dos dropdowns:**
   - Editar os `<option>` no template de `OtherRecipes.vue`
   - Garantir que os valores correspondem aos ENUMs do Supabase

3. **Modificar estilos:**
   - Todo CSS está em `<style scoped>` no `OtherRecipes.vue`
   - Usar variáveis CSS: `var(--accent-color)`, `var(--text-primary)`, etc.

### Para Usuários

1. **Encontrar receitas rápidas:**
   - Filtrar por tempo_max = 20 ou 30 minutos

2. **Encontrar receitas fáceis:**
   - Filtrar por dificuldade = `Facil` (exibe "Fácil" na UI)

3. **Maximizar uso do inventário:**
   - Marcar "Apenas ingredientes que você tem"

4. **Combinar filtros:**
   - Quanto mais filtros, mais específicos os resultados

## 🐛 Troubleshooting

### Problema: Filtros não aparecem
**Solução:** Verificar se o botão "Filtros" está visível no topo da página

### Problema: Nenhuma receita retornada
**Solução:** 
- Tentar limpar filtros
- Verificar se há receitas que atendem aos critérios
- Checar console do browser para erros

### Problema: "Apenas meus ingredientes" não funciona
**Solução:**
- Verificar se usuário está logado
- Verificar se há dados na tabela `Inventário` para o usuário
- Checar se `idUtilizador` está correto

### Problema: Backend retorna erro 500
**Solução:**
- Verificar logs do backend
- Checar se as tabelas existem no Supabase
- Verificar RLS (Row Level Security) no Supabase

## 🎉 Funcionalidades Futuras (Sugestões)

- [ ] Salvar filtros favoritos do usuário
- [ ] Filtrar por calorias totais
- [ ] Filtrar por número de ingredientes
- [ ] Busca por texto (nome ou descrição)
- [ ] Ordenação (mais recente, mais rápida, menos calorias)
- [ ] Tags personalizadas
- [ ] Filtrar por alergias/restrições alimentares

## 📝 Notas Técnicas

- **Performance:** Filtros são aplicados no backend (Supabase) para eficiência
- **UX:** Overlay fecha automaticamente após aplicar filtros
- **Mobile:** Design responsivo, funciona em dispositivos móveis
- **Acessibilidade:** Campos de formulário com labels apropriados
- **Validação:** Valores numéricos validados no frontend e backend

---

**Desenvolvido para NomNom - BugsByte '26** 🍔
**Las Lipetes Team** ✨
