<script setup lang="ts">
import { computed } from "vue";
import { CircleCheck, CircleClose, Loading, Minus } from "@element-plus/icons-vue";
import type { AgentStatus, ProgressState } from "../types/review";

const props = defineProps<{
  progressState: ProgressState;
}>();

const agentNames = ["[安全]", "[性能]", "[风格]"];

const statusText: Record<AgentStatus, string> = {
  idle: "等待中",
  running: "审查中",
  done: "已完成",
  error: "失败",
  skipped: "已跳过",
};

const statusIcon = (status: AgentStatus) => {
  if (status === "done") return CircleCheck;
  if (status === "error") return CircleClose;
  if (status === "running") return Loading;
  return Minus;
};

const percent = computed(() => Math.max(0, Math.min(100, props.progressState.percent)));
</script>

<template>
  <el-card class="analysis-progress" shadow="never">
    <header>
      <strong>{{ progressState.reconnecting ? "重新连接中..." : progressState.currentPhase || "正在准备分析" }}</strong>
      <span>{{ percent }}%</span>
    </header>
    <el-progress :percentage="percent" :stroke-width="10" :show-text="false" />
    <div class="agent-grid">
      <article
        v-for="agent in agentNames"
        :key="agent"
        :class="`status-${progressState.agents[agent] || 'idle'}`"
      >
        <div>
          <strong>{{ agent }}</strong>
          <span>{{ statusText[progressState.agents[agent] || "idle"] }}</span>
        </div>
        <small v-if="progressState.agentRisks[agent]">
          {{ progressState.agentRisks[agent].risks }} 风险 / {{ progressState.agentRisks[agent].high }} 高危
        </small>
        <el-icon :class="{ spinning: progressState.agents[agent] === 'running' }">
          <component :is="statusIcon(progressState.agents[agent] || 'idle')" />
        </el-icon>
      </article>
    </div>
  </el-card>
</template>

<style scoped lang="scss">
@use "../styles/variables" as *;

.analysis-progress {
  border: 1px solid $border;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 10px 28px rgba(30, 41, 59, 0.04);

  :deep(.el-card__body) {
    display: grid;
    gap: 14px;
    padding: 16px;
  }

  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    color: $text;
    font-size: 14px;

    span {
      color: $primary;
      font-weight: 900;
    }
  }
}

.agent-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;

  article {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 8px;
    align-items: center;
    min-height: 58px;
    padding: 10px 12px;
    border: 1px solid $line;
    border-radius: 8px;
    background: #fbfdff;

    div {
      display: grid;
      gap: 3px;
      min-width: 0;
    }

    strong {
      color: $text;
      font-size: 13px;
    }

    span,
    small {
      color: $soft;
      font-size: 11px;
    }
  }
}

.status-running { border-color: #bfdbfe; background: #eff6ff; color: $primary; }
.status-done { border-color: #bbf7d0; background: #ecfdf3; color: $success; }
.status-error { border-color: #fecaca; background: #fff7f7; color: $danger; }
.status-skipped { border-color: #e5e7eb; background: #f8fafc; color: $soft; }

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 900px) {
  .agent-grid {
    grid-template-columns: 1fr;
  }
}
</style>
