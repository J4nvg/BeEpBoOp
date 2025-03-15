# Use an official Node.js image
FROM node:24-alpine

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port (commonly 3000 for Next.js)
EXPOSE 3000

# Start the Next.js application (change command as needed, e.g., "dev" for development)
CMD ["npm", "run", "dev"]
