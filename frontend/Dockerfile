# Build stage
FROM node:14-alpine as build

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY package*.json ./
RUN npm install

# Copy all source code
COPY . .

# Build the app
RUN npm run build


# Production stage
FROM nginx:alpine

# Copy build output to Nginx default public folder
COPY --from=build /app/build /usr/share/nginx/html

# --- PERUBAHAN DIMULAI DI SINI ---

# Hapus file konfigurasi default dari Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Salin file konfigurasi kustom Anda ke dalam image
COPY nginx.conf /etc/nginx/conf.d/default.conf

# --- PERUBAHAN SELESAI ---

# Expose port 80 to the host
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]