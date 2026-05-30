import type { ReviewProgressEvent } from "../types/review";

export const phaseLabel = (
  event: ReviewProgressEvent["event"],
  phase?: string,
  agent?: string,
): string => {
  if (event === "phase_start" && phase === "phase1") return "正在分析 PR 特征";
  if (event === "phase_done" && phase === "phase1") return "PR 特征分析完成";
  if (event === "agent_start") return `${agent || ""}审查中`;
  if (event === "agent_done") return `${agent || ""}审查完成`;
  if (event === "agent_error") return `${agent || ""}审查失败`;
  if (event === "agent_skipped") return `${agent || ""}无可分析 diff，已跳过`;
  if (event === "phase_start" && phase === "phase2") return "启动专家分析";
  if (event === "phase_start" && phase === "phase3") return "正在生成最终报告";
  if (event === "phase_done" && phase === "phase3") return "报告生成完成";
  if (event === "complete") return "分析完成";
  if (event === "error") return "分析失败";
  return "";
};
