FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json /app/
RUN npm install
COPY src /app/src
RUN npm run build
CMD ["node", "dist/index.js"]


