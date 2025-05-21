FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --include=dev

COPY . .

RUN npm install react-router-dom@latest
RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]


# FROM node:20-alpine AS runner

# WORKDIR /app

# RUN npm install -g serve

# COPY --from=builder /app/dist ./dist

# EXPOSE 3000

# CMD ["serve", "-s", "dist", "--no-clipboard"]