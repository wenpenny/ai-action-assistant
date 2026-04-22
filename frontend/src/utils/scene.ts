export const sceneTypeMap = {
  schedule: {
    label: '日程',
    color: '#1989fa'
  },
  task: {
    label: '任务',
    color: '#ff9900'
  },
  travel: {
    label: '出行',
    color: '#52c41a'
  },
  other: {
    label: '其他',
    color: '#999999'
  }
};

export const getSceneLabel = (sceneType: string) => {
  return sceneTypeMap[sceneType as keyof typeof sceneTypeMap]?.label || '未知';
};

export const getSceneColor = (sceneType: string) => {
  return sceneTypeMap[sceneType as keyof typeof sceneTypeMap]?.color || '#999999';
};
