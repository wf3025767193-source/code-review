<script setup lang="ts">
import type { InsightCard } from "../types/ui";
import type { AgentStats } from "../types/review";

defineProps<{
  insightCards?: InsightCard[];
  agentStats?: Record<string, AgentStats>;
}>();
</script>

<template>
  <div class="insight-grid">
    <el-card v-for="card in insightCards || []" :key="card.title" class="panel insight-card" shadow="never">
      <h3><el-icon><component :is="card.icon" /></el-icon>{{ card.title }}</h3>
      <p v-for="row in card.rows" :key="row">{{ row }}</p>
    </el-card>
    <el-card v-for="source in ['安全', '性能', '风格']" :key="source" class="panel insight-card agent-card" shadow="never">
      <h3>{{ source }}审查</h3>
      <strong>{{ agentStats?.[source]?.risks || 0 }} 风险</strong>
      <p>{{ agentStats?.[source]?.high || 0 }} 高危</p>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
@use "../styles/variables" as *;

.insight-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  min-height: 0;
}

.panel {
  border: 1px solid $border;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 10px 28px rgba(30, 41, 59, 0.04);

  :deep(.el-card__body) {
    height: 100%;
    padding: 16px;
  }
}

.insight-card {
  h3 {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 0;
    color: $text;
    font-size: 15px;
    font-weight: 800;
  }

  p {
    margin: 12px 0 0;
    color: $muted;
    font-size: 12px;
    line-height: 1.55;
  }
}

.agent-card strong {
  display: block;
  margin-top: 12px;
  color: $text;
  font-size: 20px;
}
</style>
