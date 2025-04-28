import "./App.css";
import DailyLog from "@/components/daily-log";

function App() {
  return (
    <>
      <main className="h-screen w-screen grid grid-cols-3 gap-4 m-auto p-8">
        <DailyLog />
        <div className="col-span-1 border border-green-700 rounded-md">2</div>
        <div className="col-span-1 border border-green-700 rounded-md">3
        </div>
        <div className="col-span-1 border border-green-700 rounded-md">4</div>
        <div className="col-span-1 border border-green-700 rounded-md">5</div>
      </main>
    </>
  );
}

export default App;
