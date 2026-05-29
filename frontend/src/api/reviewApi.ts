import type { ReviewAnalyzeResponse } from "../types/review";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";
const REVIEW_API_TOKEN = import.meta.env.VITE_REVIEW_API_TOKEN;

interface ApiErrorBody {
  detail?: unknown;
}

export async function analyzePullRequest(
  prUrl: string,
): Promise<ReviewAnalyzeResponse> {
  if (!REVIEW_API_TOKEN) {
    throw new Error("VITE_REVIEW_API_TOKEN 未配置");
  }

  const response = await fetch(`${API_BASE_URL}/review/analyze`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${REVIEW_API_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prUrl }),
  });

  if (!response.ok) {
    let message = `请求失败：${response.status}`;
    try {
      const body = (await response.json()) as ApiErrorBody;
      if (typeof body.detail === "string") {
        message = body.detail;
      } else if (Array.isArray(body.detail)) {
          message = "请求参数格式不正确";
      }
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  return (await response.json()) as ReviewAnalyzeResponse;
}
