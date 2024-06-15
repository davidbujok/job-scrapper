import { useState } from "react";
import Jobs from "./Components/Jobs";
import { Job as JobType } from "./Interfaces";
import JobComponent from "./Components/JobComponent";
import Navbar from "./Components/Navbar";

function App() {
  const [job, setJob] = useState<JobType | null>(null);
  const [jobs, setJobs] = useState<Array<JobType>>([]);

  return (
    <>
      <Navbar setJobs={setJobs} />
      <div className="flex ml-11 gap-14 ">
        <div className="">
          <Jobs setJob={setJob} jobs={jobs} setJobs={setJobs}></Jobs>
        </div>
        <div className="w-2/5">{job && <JobComponent job={job} />}</div>
      </div>
    </>
  );
}

export default App;
