FROM node:20.12.2-bookworm AS build
# ARG NODE_ENV=production
WORKDIR /app
COPY package.json /app/package.json
COPY pnpm-lock.yaml /app/pnpm-lock.yaml
RUN corepack pnpm install
COPY . .
RUN corepack pnpm run build

FROM nginx:1.21.4-alpine AS production
ENV NODE_ENV production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
