FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --production=false

COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app

RUN npm install --production

COPY --from=0 /app/.next ./.next
COPY --from=0 /app/public ./public
COPY --from=0 /app/package.json ./

EXPOSE 3000
CMD ["npm", "start"]
