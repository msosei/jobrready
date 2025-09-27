# Use Node.js 18 Alpine image as the base image
# This provides a lightweight foundation with Node.js installed
FROM node:18-alpine

# Set the working directory inside the container
# All subsequent commands will be executed relative to this directory
WORKDIR /app

# Copy package files to the container
# This includes package.json and package-lock.json for dependency management
COPY package.json package-lock.json ./

# Install npm dependencies
# Uses legacy peer dependencies to avoid compatibility issues
RUN npm ci --legacy-peer-deps

# Copy all source code to the container
# This includes all files needed to run the frontend application
COPY . .

# Expose port 3000 to allow external access to the application
# This is the port Vite will use for the development server
EXPOSE 3000

# Define the command to run the application when the container starts
# Uses npm to run the development script with host and port configuration
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]