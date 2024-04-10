import { useState } from "react"
import Jobs from "./Components/Jobs"
import { Job as JobType } from "./Interfaces"
import JobComponent from "./Components/JobComponent"
import Navbar from "./Components/Navbar"

function App() {

  //const [visible, setVisible] = useState<boolean>(false)
  const [job, setJob] = useState<JobType | null>(null)

  return (
    <>
      <Navbar />
      <div className="flex ml-11 gap-14">
        <div className="flex-col w-4/12">
          <Jobs setJob={setJob}></Jobs>
        </div>
        <div className="w-2/5">
        {job &&
          <JobComponent job={job} />
        }
        </div>
      </div>
    </>
  )
}

export default App
