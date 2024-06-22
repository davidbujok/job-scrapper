import { Dispatch, SetStateAction, useState } from "react";
import { Job as JobType } from "../Interfaces"
import ScrapeJobs from "./ScrapeJobs";

interface JobProps {
    setJobs: Dispatch<React.SetStateAction<JobType[]>>
    jobs: JobType[]
    setScrapePage: React.Dispatch<React.SetStateAction<boolean>>;
    setDocsPage: Dispatch<SetStateAction<boolean>>;
}

export default function Navbar({ setJobs, jobs, setDocsPage }: JobProps) {

    const [query, setQuery] = useState<string>("")
    const originalJobs = jobs
    const [scrapePage, setScrapePage] = useState<boolean>(false)

    const searchJobs = (query: string) => {
        setQuery(query);
        if (query === "") {
            setJobs(originalJobs);
        } else {
            const filteredJobs = originalJobs.filter(job =>
                job.title.toLowerCase().includes(query.toLowerCase()) ||
                job.position.toLowerCase().includes(query.toLowerCase())
            );
            setJobs(filteredJobs);
        }
    };

    //async function queryJobs(query: String) {
    //    console.log(query)
    //    const response = await fetch(`http://127.0.0.1:5000/junior_jobs/${query}`);
    //    const queried_jobs = await response.json()
    //    setJobs(queried_jobs)
    //}

    //async function fetchJobs() {
    //    const response = await fetch("http://127.0.0.1:5000/jobs");
    //    const jobs = await response.json()
    //    setJobs(jobs)
    //}

    //async function searchJobs(e: string) {
    //    //e?.preventDefault();
    //    setQuery(e)
    //    query ? queryJobs(query) : fetchJobs()
    //}

    //<button onClick={activateScraping}>Start Scraping Data</button>
    return (
        <>
            {scrapePage ? <ScrapeJobs setScrapePage={setScrapePage} /> :
                <div className="flex bg-amber-800 justify-between mb-5 pt-2 h-20">
                    <div className="flex gap-10 ml-10">
                        <form>
                            <p className="text-white">Search your jobs</p>
                            <input className="w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                                value={query}
                                onChange={(e) => searchJobs(e.target.value)}
                            />
                        </form>
                    </div>
                    <button
                        onClick={() => setDocsPage(false)}
                    >
                        <h1 className="text-4xl text-green-200 font-extrabold">
                            Workless
                        </h1>
                    </button>
                    <div className="self-center mr-5 text-green-100 text-xl">
                        <button onClick={() => setScrapePage(true)}>Scrape Jobs</button>
                    </div>
                </div>
            }
        </>
    )
}
