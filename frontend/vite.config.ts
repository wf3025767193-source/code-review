import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import type { ClientRequest, IncomingMessage, ServerResponse } from "http";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiProxyTarget = env.VITE_API_PROXY_TARGET || "http://127.0.0.1:8000";
  const reviewApiToken = env.REVIEW_API_TOKEN || "";

  return {
    plugins: [vue()],
    server: {
      proxy: {
        "/api": {
          target: apiProxyTarget,
          changeOrigin: true,
          configure: (proxy) => {
            proxy.on("proxyReq", (proxyReq: ClientRequest, _req: IncomingMessage, _res: ServerResponse) => {
              if (reviewApiToken) {
                proxyReq.setHeader("Authorization", `Bearer ${reviewApiToken}`);
              }
            });
          },
        },
      },
    },
  };
});
