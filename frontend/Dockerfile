FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

COPY . .

# La URL de la API se hornea en el build estático (cámbiala al desplegar)
ARG PUBLIC_API_URL=http://localhost:8000
ENV PUBLIC_API_URL=$PUBLIC_API_URL
RUN npm run build

EXPOSE 4321
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4321"]
