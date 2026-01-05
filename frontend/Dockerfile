# Multi-stage build for the frontend
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Copy nginx config explicitly
COPY nginx.conf /app/nginx.conf

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Install curl for health check
RUN apk add --no-cache curl

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration (already in /app from builder stage)
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
