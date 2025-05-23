# Zuno Marketplace

## Complete Automation

When you run:

```bash
docker-compose up
```

The system will automatically:

1. Launch the Tor container and set up a hidden service
2. Start the FastAPI backend which will:
   - Generate the Tor configuration
   - Wait for and display the .onion link in the terminal
3. Launch the Next.js frontend

### Viewing Your .onion Link

You can view your marketplace's .onion link in two ways:

1. **Terminal Output**: The link will be displayed in the backend container's logs
2. **Web Interface**: Visit `/onion` in your browser for a modern UI displaying the link

### Technical Details

- The backend automatically polls for the .onion hostname file
- All services are properly orchestrated through Docker Compose
- Secure volume sharing between Tor and backend containers
- Modern, responsive UI for displaying the .onion link

A secure marketplace platform built with Next.js, FastAPI, and Tor network integration.

## Services

The application consists of three main services:

1. **Tor Service**: Handles .onion link setup and Tor network integration
2. **Backend Service**: FastAPI server providing the API endpoints
3. **Frontend Service**: Next.js application for the vendor interface

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.10+ (for local development)

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zuno-marketplace.git
cd zuno-marketplace
```

2. Start the services using Docker Compose:
```bash
docker-compose up --build
```

This will start all three services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Tor: Port 9050 (SOCKS proxy)

## Service Details

### Frontend (Next.js)
- Modern UI with Tailwind CSS
- Responsive design
- Vendor dashboard
- Product management interface

### Backend (FastAPI)
- RESTful API
- Product management endpoints
- Secure authentication
- Error handling

### Tor Service
- .onion link generation
- Secure network routing
- Anonymous access

## Development

To run services individually for development:

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Tor
```bash
cd tor
docker build -t tor-service .
docker run -p 9050:9050 -p 9051:9051 tor-service
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for the Swagger UI documentation.

## Security Considerations

- The Tor service provides anonymity for marketplace access
- All API endpoints use HTTPS in production
- Frontend uses secure authentication
- Sensitive data is encrypted

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
