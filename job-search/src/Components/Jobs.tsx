import { useEffect, useState } from "react"
import { Job } from "../Interfaces";

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


const Jobs = () => {

  const [jobs, setJobs] = useState<Array<Job>>([])

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

  const toggleToggle = (index: number) => {
	  const jobsCopy = [...jobs]
	  const job = jobsCopy[index]
	  console.log( job.apply_status )
	  job.apply_status = job.apply_status ? false : true
	  console.log( job.apply_status )
	  jobsCopy[index] = job
	  setJobs(jobsCopy)
  }

  useEffect(() => {
    fetchJobs()
    fetchJuniorJobs()
  }, [])


  return (
    <>
      <h1>Jobs</h1>
      {jobs?.map((job, index) => (
        <div onClick={() => console.log( "You clicked" )} key={job.id}>
          <p>{job.title} | {job.company}  | {job.id} </p>
          <input onClick={() => toggleToggle(index)} type="checkbox"></input>
          {job.apply_status ? <p>True</p> : <p>False</p>}
        </div>
      ))
      }
    </>
  )
}

export default Jobs
