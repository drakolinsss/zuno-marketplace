# Use official Node.js LTS image
FROM node:18-alpine

# Create app directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Copy app source
COPY . .

# Remove dev dependencies and cache
RUN npm prune --production && npm cache clean --force

# Set environment variables for security
ENV NODE_ENV=production
ENV NO_JS_TRACKING=1
ENV NO_COOKIES=1
ENV NO_IP_LOGS=1

# Expose port for Next.js app
EXPOSE 3000

# Start the app
CMD ["npm", "run", "start"]
