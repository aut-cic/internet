FROM banian/node

# Copy dependencies in seperate layers
COPY package.json yarn.lock /usr/src/app/
RUN NODE_ENV=production yarn

# Copy source
COPY . /usr/src/app/

# Build
#RUN yarn build

# Run tests
#RUN yarn test