import { Dispatch, FormEvent, SetStateAction, useEffect, useState } from "react"
import { Job as JobType } from "../Interfaces";
import Navbar from "./Navbar";


// fetch("http://127.0.0.1:5000/update-job", {
//   method: "POST",
//   body: JSON.stringify({
//     id: number;
//     title: string;
//     position: string;
//     company: string;
//     location: string;
//     about: string;
//     url: string;
//     job_id: number;
//     post_date: string;
//     apply_status: boolean;
//     websites_id: number;
//   }),
//   headers: {
//     "Content-type": "application/json; charset=UTF-8"
//   }
// })
//   .then((response) => response.json())
//   .then((json) => console.log(json));
interface JobsProps {
  setJob: Dispatch<SetStateAction<JobType | null>>;
}

const Jobs = ({ setJob }: JobsProps) => {

  const [jobs, setJobs] = useState<Array<JobType>>([])
  const [query, setQuery] = useState<string>("")

  async function fetchJobs() {
    const response = await fetch("http://127.0.0.1:5000/jobs");
    const jobs = await response.json()
    setJobs(jobs)
  }

  async function fetchJuniorJobs() {
    const response = await fetch("http://127.0.0.1:5000/junior_jobs");
    const junior_jobs = await response.json()
    setJobs(junior_jobs)
  }

  async function queryJobs(query: String) {
    const response = await fetch(`http://127.0.0.1:5000/junior_jobs/${query}`);
    const queried_jobs = await response.json()
    setJobs(queried_jobs)
  }

  const toggleToggle = (index: number) => {
    const jobsCopy = [...jobs]
    const job = jobsCopy[index]
    console.log(job.apply_status)
    job.apply_status = job.apply_status ? false : true
    console.log(job.apply_status)
    jobsCopy[index] = job
    setJobs(jobsCopy)
  }

  useEffect(() => {
    fetchJobs()
    fetchJuniorJobs()
  }, [])

  async function searchJobs(event: FormEvent<HTMLFormElement>) {
    event?.preventDefault();
    query ? queryJobs(query) : null
    console.log("HERE")
  }

  return (
    <>
      <form onSubmit={searchJobs}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </form>
      {query && 
        <p>{query}</p>
      }
      {jobs?.map((job, index) => (
        <div onClick={() => setJob(job)} key={job.id} className="mb-2">
          <p>{job.title} | {job.company}
            <input className="ml-3" onClick={() => toggleToggle(index)} type="checkbox"></input>
          </p>
        </div>
      ))
      }
    </>
  )
}

export default Jobs
