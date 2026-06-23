import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    unoptimized: true,
  },
  async rewrites() {
    // In Docker the backend is at http://backend:8000
    // In local dev (XAMPP / npm run dev) it is at http://localhost:5000
    const backendUrl =
      process.env.BACKEND_URL ||          // set this in docker-compose for server-side
      process.env.NEXT_PUBLIC_API_URL ||   // fallback from .env.local
      "http://localhost:5000";

    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
