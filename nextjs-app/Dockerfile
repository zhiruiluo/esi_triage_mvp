FROM node:20-alpine

WORKDIR /app

COPY nextjs-app/package.json nextjs-app/package-lock.json* ./
RUN npm install

COPY nextjs-app/. .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
