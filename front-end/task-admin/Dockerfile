FROM node:16-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .
RUN npm run build

# Expose the port Vite uses
EXPOSE 5173 4173

# Run the Vite development server
CMD ["npm", "run", "dev"]