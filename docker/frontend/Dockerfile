FROM node:16

WORKDIR /star_burger

COPY ./package.json .

COPY ./package-lock.json .

RUN npm ci --dev

COPY ./bundles-src ./bundles-src
