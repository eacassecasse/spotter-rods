import React, { useMemo } from 'react';

interface DayLogProps {
  isActive: boolean;
  position: 'top' | 'bottom';
  startPos?: number; // Minutes (0-59)
  endPos?: number;   // Minutes (0-59)
}

const BORDER_CONFIG = {
  top: {
    rightBorders: [0, 1, 2, 4, 5, 6, 9], // Indices with gray right borders
    activeRows: [1, 2]                    // Rows where active time blocks appear
  },
  bottom: {
    rightBorders: [5, 8, 9, 10, 12, 13, 14],
    activeRows: [1, 2]
  }
};

export default function DayLog({ position, isActive, startPos, endPos }: DayLogProps) {
  const getColumnFromTime = (time?: number) => {
    if (time === undefined) return -1;
    return Math.floor((time % 60) / 15);
  };

  const redBorderRows = useMemo(() => {
    if (!isActive || startPos === undefined || endPos === undefined) return [];

    const startCol = getColumnFromTime(startPos);
    const endCol = getColumnFromTime(endPos);
    if (startCol !== endCol) return [];

    const isForward = endPos > startPos;
    const activeRows = BORDER_CONFIG[position].activeRows;

    return isForward
      ? activeRows.filter(row => row >= Math.floor(startPos / 60)) // Extend downward
      : activeRows.filter(row => row <= Math.floor(startPos / 60)); // Extend upward
  }, [isActive, startPos, endPos, position]);

  return (
    <div 
      className="grid grid-cols-4 grid-rows-4 border"
      role="grid"
      aria-label={`Time slots for ${position} segment`}
    >
      {Array.from({ length: 16 }, (_, index) => {
        const col = index % 4;
        const row = Math.floor(index / 4);
        const borderClasses = [];

        if (BORDER_CONFIG[position].rightBorders.includes(index) && col < 3) {
          borderClasses.push('border-r-2 border-gray-300');
        }

        // Red bottom border (start position marker)
        if (isActive && BORDER_CONFIG[position].activeRows.includes(row)) {
          const startCol = getColumnFromTime(startPos);
          if (col === startCol && row === 1) {
            borderClasses.push('border-b-2 border-b-red-500');
          }
        }

        // Red right border (end position, extended vertically)
        if (redBorderRows.includes(row) && col === getColumnFromTime(endPos)) {
          borderClasses.push('border-r-2 border-r-red-500');
        }

        return (
          <div
            key={`cell-${row}-${col}`}
            className={borderClasses.join(' ')}
            role="gridcell"
            aria-label={`${row * 15 + col * 15} minutes`}
          />
        );
      })}
    </div>
  );
}