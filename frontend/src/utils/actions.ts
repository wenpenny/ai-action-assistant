export const getActionLabel = (action: string): string => {
  const labels: Record<string, string> = {
    create_todo: '创建待办',
    set_reminder: '设置提醒',
    open_map: '打开地图',
    export_calendar: '导出日历'
  };
  return labels[action] || action;
};

export const getActionIcon = (action: string): string => {
  const icons: Record<string, string> = {
    create_todo: 'todo-list',
    set_reminder: 'clock',
    open_map: 'location',
    export_calendar: 'calendar'
  };
  return icons[action] || 'star';
};