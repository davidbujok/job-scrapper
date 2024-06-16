import { Dispatch, useState } from "react";
import { Job as JobType } from "../Interfaces"

interface JobProps {
    setJobs: Dispatch<React.SetStateAction<JobType[]>>
}

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
            <div className="flex bg-stone-300 justify-between mb-5 pt-2">
                <div className="flex gap-10 ml-10">
                    <form>
                        <input className="w-full bg-stone-400 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            value={query}
                            onChange={(e) => searchJobs(e)}
                        />
                    </form>
                </div>
                <h1 className="text-5xl left-1/2 justify-self-center text-amber-900 font-extrabold">Workless</h1>
                <div className="self-center mr-5 text-3xl">
                    <button onClick={activateScraping}>Start Scraping Data</button>
                </div>
            </div>
        </>
    )
}
