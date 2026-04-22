export const getSceneLabel = (scene: string): string => {
  const labels: Record<string, string> = {
    schedule: '日程',
    task: '任务',
    travel: '出行',
    unknown: '未知'
  };
  return labels[scene] || scene;
};

export const getSceneColor = (scene: string): string => {
  const colors: Record<string, string> = {
    schedule: '#1890ff',
    task: '#faad14',
    travel: '#52c41a',
    unknown: '#999'
  };
  return colors[scene] || '#999';
};