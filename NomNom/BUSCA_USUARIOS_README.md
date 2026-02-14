# 🔍 Página de Busca de Usuários - Frontend

## O que foi criado

Uma página completa para buscar, listar e gerenciar usuários da base de dados do Account Management API.

## 📁 Arquivos Criados

### 1. **src/api/client.js**
Cliente Axios configurado para comunicação com a API
- Configuração de base URL
- Interceptor automático de tokens
- Headers padrão

### 2. **src/composables/useUsers.js**
Composable Vue 3 para gerenciar usuários
- `getUser(userId)` - Buscar usuário por ID
- `listUsers()` - Listar todos os usuários
- `createUser()` - Criar novo usuário
- `updateUser()` - Atualizar usuário
- `deleteUser()` - Deletar usuário
- Estado reativo: `users`, `currentUser`, `loading`, `error`

### 3. **src/pages/SearchUser.vue**
Página completa com interface para:
- 🔍 **Buscar** usuário por ID
- 📋 **Listar** todos os usuários com paginação
- ✏️ **Editar** informações do usuário
- 🗑️ **Deletar** usuário
- 📊 **Visualizar** detalhes (nome, email, data de criação)

## 🚀 Como Usar

### Step 1: Instalar Dependências

```bash
cd NomNom
npm install
```

O Axios será instalado automaticamente.

### Step 2: Iniciar o Servidor Frontend

```bash
npm run dev
```

A aplicação abrirá em: `http://localhost:5173`

### Step 3: Usar a Página

1. Clique em "Buscar Usuário" na navegação
2. Digite um ID de usuário ou clique em "Carregar Usuários" para listar
3. Clique em "Ver Detalhes" para buscar um usuário específico
4. Use os botões:
   - ✏️ **Editar** - Modificar nome e email
   - 🗑️ **Deletar** - Remover usuário

## 📋 Interface

### Seção da Esquerda: Busca Individual
```
┌─────────────────────────────────┐
│   Buscar Usuário                │
├─────────────────────────────────┤
│                                 │
│  [Digite ID] [Buscar]           │
│                                 │
│  ┌───────────────────────────┐  │
│  │ Nome do Usuário           │  │
│  │ ID: abc-123-def           │  │
│  │                           │  │
│  │ Email: user@exemplo.com   │  │
│  │ Criado: 14/02/2026 10:30  │  │
│  │                           │  │
│  │ [Deletar] [Editar]        │  │
│  └───────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

### Seção da Direita: Listar Usuários
```
┌─────────────────────────────────┐
│   Listar Usuários               │
├─────────────────────────────────┤
│                                 │
│    [Carregar Usuários]          │
│                                 │
│  ┌─────────────────────────┐   │
│  │ João Silva              │   │
│  │ joao@example.com        │   │
│  │            [Ver...]     │   │
│  └─────────────────────────┘   │
│                                 │
│  ┌─────────────────────────┐   │
│  │ Maria Santos            │   │
│  │ maria@example.com       │   │
│  │            [Ver...]     │   │
│  └─────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

## 🎨 Estilos

- **Cores**: Gradiente Roxo-Azul (#667eea - #764ba2)
- **Layout**: Grid 2 colunas (responsivo em mobile)
- **Componentes**: Cards elegantes com sombras
- **Interatividade**: Transições suaves e feedback visual

## 📱 Responsividade

A página é totalmente responsiva:
- **Desktop** (>768px): 2 colunas lado a lado
- **Mobile** (<768px): 1 coluna empilhada

## 🔗 Estrutura de Dados

### Usuário Retornado da API
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "João Silva",
  "email": "joao@example.com",
  "created_at": "2026-02-14T10:30:00Z"
}
```

## ⚙️ Configuração

### CORS
O frontend em `http://localhost:5173` precisa de CORS liberado no backend. Já está configurado em:
`account-management-api/src/main.py`

### Variáveis de Ambiente
O frontend conecta automaticamente a:
```
http://localhost:8000
```

Para trocar, edite em `src/api/client.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000'; // Edite aqui
```

## 🛠️ Funcionalidades Implementadas

### ✅ Busca de Usuário
- Campo de entrada para ID
- Busca ao pressionar Enter ou clicar em "Buscar"
- Exibição de detalhes completos
- Tratamento de erros

### ✅ Edição de Usuário
- Formulário inline para editar nome e email
- Validação básica
- Mensagem de sucesso/erro

### ✅ Deleção de Usuário
- Confirmação antes de deletar
- Remoção automática da lista
- Mensagem de sucesso

### ✅ Listagem de Usuários
- Carregamento de todos os usuários
- Display em cards elegantes
- Link direto para visualizar detalhes
- Paginação prepare (limit/offset)

### ✅ Estado Reativo
- Indicador de carregamento (loading)
- Mensagens de erro personalizadas
- Estado do formulário de edição

## 📝 Exemplo de Uso

### Buscar um Usuário
1. Cole o ID: `550e8400-e29b-41d4-a716-446655440000`
2. Clique em "Buscar"
3. Veja os detalhes aparecer

### Editar um Usuário
1. Após buscar, clique em "Editar"
2. Modifique o nome e/ou email
3. Clique em "Salvar Alterações"

### Deletar um Usuário
1. Após buscar, clique em "Deletar Usuário"
2. Confirme na dialog
3. Usuário será removido

## 🐛 Troubleshooting

### "Erro ao buscar usuário"
- Verifique se o backend está rodando em `http://localhost:8000`
- Verifique o ID digitado
- Consulte console do navegador (F12) para mais detalhes

### CORS Error
- Certifique-se que o backend tem CORS habilitado
- Reinicie ambas as aplicações

### Conexão Recusada
- Backend não está rodando
- URL incorreta em `src/api/client.js`

## 🚀 Próximas Melhorias

- [ ] Adicionar busca por nome/email
- [ ] Paginação visual
- [ ] Exportar dados para CSV
- [ ] Filtros avançados
- [ ] Dark mode
- [ ] Notificações toast
- [ ] Upload de avatar

## 📚 Referências

- [Vue 3 Documentation](https://vuejs.org/)
- [Axios Documentation](https://axios-http.com/)
- [Vite Documentation](https://vitejs.dev/)

---

**Status**: ✅ Completo e Funcional
**Última Atualização**: 14/02/2026
