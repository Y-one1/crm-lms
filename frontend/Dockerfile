FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Запуск Vite с флагом --host, чтобы контейнер отвечал наружу
CMD ["npm", "run", "dev", "--", "--host"]