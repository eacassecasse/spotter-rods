import { formatDate } from "date-fns";

export const getTime = (strDate: string) => {
  const date = new Date(strDate);
  const time = formatDate(date, "hh:mm");
  const parsedTime = time.split(":");

  return parsedTime;
};
