/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    // Strip /api/v2 to get the backend origin (e.g. http://backend:8000)
    const backendBase = (
      process.env.NEXT_PUBLIC_WAGTAIL_API_URL || "http://127.0.0.1:8000/api/v2"
    ).replace(/\/api\/v2\/?$/, "");

    return [
      {
        // Proxy all /media/* requests to the Django backend so browsers can
        // load images using relative URLs returned by the Wagtail API.
        source: "/media/:path*",
        destination: `${backendBase}/media/:path*`,
      },
    ];
  },
};

export default nextConfig;
