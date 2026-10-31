import type { NextConfig } from "next";

const isGithubPages = process.env.GITHUB_ACTIONS === "true" || !!process.env.NEXT_PUBLIC_BASE_PATH;
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || (process.env.GITHUB_ACTIONS === "true" ? "/exorcist-exe" : "");

const nextConfig: NextConfig = {
  output: isGithubPages ? "export" : undefined,
  basePath: basePath || undefined,
  assetPrefix: basePath || undefined,
  images: {
    unoptimized: true,
  },
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  async rewrites() {
    if (isGithubPages) return [];
    const rawTarget = process.env.BACKEND_URL || process.env.BACKEND_HOST;
    let backendTarget = "http://127.0.0.1:8000";
    if (rawTarget) {
      if (rawTarget.startsWith("http://") || rawTarget.startsWith("https://")) {
        backendTarget = rawTarget.replace(/\/$/, "");
      } else if (rawTarget.includes(":")) {
        backendTarget = `http://${rawTarget}`;
      } else {
        const port = process.env.BACKEND_PORT || "10000";
        backendTarget = `http://${rawTarget}:${port}`;
      }
    }
    return [
      {
        source: "/api/game/:path*",
        destination: `${backendTarget}/api/game/:path*`,
      },
      {
        source: "/api/status",
        destination: `${backendTarget}/api/status`,
      },
    ];
  },
};

export default nextConfig;
