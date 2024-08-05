FROM node:14

WORKDIR /app

COPY package*.json ./
RUN bun install

COPY . .

CMD ["bun", "run", "dev"]
