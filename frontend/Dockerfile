# Dockerfile para o Frontend do MILAPP
FROM node:18-alpine

# Define variáveis de ambiente
ENV NODE_ENV=development
ENV CI=true

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY package*.json ./

# Instala dependências
RUN npm ci --only=production && npm cache clean --force

# Copia código da aplicação
COPY . .

# Cria usuário não-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Muda permissões
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expõe porta
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Comando para executar a aplicação
CMD ["npm", "start"]