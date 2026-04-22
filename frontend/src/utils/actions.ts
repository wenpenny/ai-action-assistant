export const actionTypeMap = {
  create_todo: {
    label: '创建待办',
    icon: 'todo-list'
  },
  set_reminder: {
    label: '设置提醒',
    icon: 'bell'
  },
  open_map: {
    label: '打开地图',
    icon: 'location'
  },
  export_calendar: {
    label: '导出日历',
    icon: 'calendar'
  }
};

export const getActionLabel = (actionType: string) => {
  return actionTypeMap[actionType as keyof typeof actionTypeMap]?.label || '未知动作';
};

export const getActionIcon = (actionType: string) => {
  return actionTypeMap[actionType as keyof typeof actionTypeMap]?.icon || 'help-o';
};
