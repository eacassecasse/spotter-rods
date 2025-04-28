import DayLog from "@/components/day-log";
import { getTime } from "@/utils/utils";
import { useMemo, useState } from "react";

const dutyStatuses = {
  "": "",
  OFF_DUTY: "Off Duty",
  ON_DUTY: "On Duty",
  DRIVING: "Driving",
  SLEEPER_BERTH: "Sleeper Berth"
} as const;

type DutyStatus = keyof typeof dutyStatuses;

interface LogEntry {
  start_datetime: string;
  end_datetime: string;
  status: DutyStatus;
  location: string;
}

const fmcsaCompliantDaylogs: LogEntry[] = [
  {
    start_datetime: "06:00",
    end_datetime: "07:30",
    status: "OFF_DUTY",
    location: "Home Terminal"
  },
  {
    start_datetime: "07:30",
    end_datetime: "08:00",
    status: "ON_DUTY",
    location: "Home Terminal"
  },
  {
    start_datetime: "08:00",
    end_datetime: "11:30",
    status: "DRIVING",
    location: "Route I-95 N"
  },
  {
    start_datetime: "11:30",
    end_datetime: "12:00",
    status: "ON_DUTY",
    location: "Rest Area MM 142"
  },
  {
    start_datetime: "12:00",
    end_datetime: "12:30",
    status: "OFF_DUTY",
    location: "Rest Area MM 142"
  },
  {
    start_datetime: "12:30",
    end_datetime: "13:00",
    status: "ON_DUTY",
    location: "Rest Area MM 142"
  },
  {
    start_datetime: "13:00",
    end_datetime: "16:30",
    status: "DRIVING",
    location: "Route I-95 N"
  },
  {
    start_datetime: "16:30",
    end_datetime: "17:00",
    status: "ON_DUTY",
    location: "Delivery Dock B"
  },
  {
    start_datetime: "17:00",
    end_datetime: "18:00",
    status: "OFF_DUTY",
    location: "Truck Stop"
  },
  {
    start_datetime: "18:00",
    end_datetime: "19:30",
    status: "SLEEPER_BERTH",
    location: "Truck Stop"
  },
  {
    start_datetime: "19:30",
    end_datetime: "20:00",
    status: "ON_DUTY",
    location: "Truck Stop"
  },
  {
    start_datetime: "20:00",
    end_datetime: "22:00",
    status: "DRIVING",
    location: "Route I-95 S"
  },
  {
    start_datetime: "22:00",
    end_datetime: "06:00+1", // Next day
    status: "SLEEPER_BERTH",
    location: "Rest Area MM 87"
  }
];

export default function DailyLog() {
  const [startPos, setStartPos] = useState<number | undefined>()
  const [endPos, setEndPos] = useState<number | undefined>()
  return (
    <div className="col-span-2 border border-green-700 rounded-md">
      <div className="grid grid-cols-7 w-full p-4 h-full border border-emerald-500">
        <div className="col-span-1 grid grid-rows-5">
          {Object.values(dutyStatuses).map((val) => {
            return (
              <div className="flex justify-center items-center self-center text-center text-wrap">
                {val}
              </div>
            );
          })}
        </div>
        <div className="col-span-6 grid grid-rows-5">
          <div className="row-span-1 grid grid-cols-[repeat(24,_minmax(0,_1fr))]">
            {Array.from({ length: 24 }, (_, i) => {
              const hour = i % 12;
              const isPM = i >= 12;
              let displayText;

              if (hour === 0) {
                displayText = isPM ? "N" : "M";
              } else {
                displayText = `${hour}`;
              }
              return (
                <div
                  className={`flex justify-center items-center self-center ${hour === 0 && "font-bold"
                    } text-center`}
                >
                  {displayText}
                </div>
              );
            })}
          </div>
          <div className="row-span-4 grid grid-cols-[repeat(24,_minmax(0,_1fr))] border border-muted">
            {Array.from({ length: 96 }, (_, index) => {
              const row = Math.floor(index / 24);

              fmcsaCompliantDaylogs.map((daylog) => {
                const parsedStartDatetime = daylog.start_datetime && getTime(daylog.start_datetime)
                const parsedEndDatetime = daylog.end_datetime && getTime(daylog.end_datetime)

                setStartPos(parseInt(parsedStartDatetime[1]))
              })

              return <DayLog key={`daily_${index}`} position={ row < 2 ? "top" : "bottom"} isActive={true}
                startPos={startPos} />;
            })}
          </div>
        </div>
      </div>
    </div>
  );
}