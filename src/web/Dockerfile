FROM node:18.17.1-alpine3.18 AS build
ENV NODE_ENV production
WORKDIR /app
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json
RUN npm install --no-cache --production
COPY . .
RUN npm run build

FROM nginx:1.21.4-alpine AS production
ENV NODE_ENV production
COPY --from=build /app/build /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
