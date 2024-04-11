import { Dispatch, useState } from "react";
import { Job as JobType } from "../Interfaces"

interface JobProps {
  setJobs: Dispatch<React.SetStateAction<JobType[]>>}

export default function Navbar({ setJobs }: JobProps) {

  const [query, setQuery] = useState<string>("")

  async function queryJobs(query: String) {
    console.log(query)
    const response = await fetch(`http://127.0.0.1:5000/junior_jobs/${query}`);
    const queried_jobs = await response.json()
    setJobs(queried_jobs)
  }
  
  async function fetchJobs() {
    const response = await fetch("http://127.0.0.1:5000/jobs");
    const jobs = await response.json()
    setJobs(jobs)
  }

  const activateScraping = () => {
    fetch("http://127.0.0.1:5000/runscript")
  }

  async function searchJobs(e: React.ChangeEvent<HTMLInputElement>) {
    e?.preventDefault();
    setQuery(e.target.value)
    query ? queryJobs(query) : fetchJobs()
  }

  return (
    <>
      <div className="flex self-center mb-5 gap-10 pt-2">
        <div className="ml-10">
          <form>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={query}
              onChange={(e) => searchJobs(e)}
            />
          </form>
          <p>{query}</p>
        </div>
        <button onClick={activateScraping}>Start Scraping Data</button>
        <h1 className="text-3xl ml-60">Jobs</h1>
      </div>
    </>
  )
}
