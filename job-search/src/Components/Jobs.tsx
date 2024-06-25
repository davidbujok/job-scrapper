import { Dispatch, useCallback, useEffect, useState } from "react";
import { Job as JobType } from "../Interfaces";
import { titleCleaner as tc } from "../helpers/text_formaters.tsx"

interface JobsProps {
    setJob: Dispatch<React.SetStateAction<JobType | null>>;
    setJobs: Dispatch<React.SetStateAction<JobType[]>>;
    jobs: JobType[];
}

const Jobs = ({ setJob, jobs, setJobs }: JobsProps) => {
    const [toggleHide, setToggleHide] = useState<boolean>(false)
    const [clickedJob, setClickedJob] = useState<JobType | null>(null);
    const [query, setQuery] = useState<string>("")
    const [firstFetch, setFirstFetch] = useState<JobType[]>([])

    const handleClick = (job: JobType) => {
        setJob(job)
        setClickedJob(job);
    };

    const searchJobs = (query: string) => {
        setQuery(query);
        if (query === "") {
            setJobs(firstFetch);
        } else {
            const filteredJobs = firstFetch.filter(job =>
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

    const fetchJobs = useCallback(async () => {
        const response = await fetch("http://127.0.0.1:5000/jobs");
        const jobsData = await response.json();
        setJobs(jobsData);
        setFirstFetch(jobsData)
    }, [setJobs]);


    const hideJob = async (jobId: number) => {
        await fetch(`http://127.0.0.1:5000/hide_job/${jobId}`);
        setToggleHide(prev => !prev);  // Toggle the value to ensure state change
    }

    useEffect(() => {
        fetchJobs();
    }, [toggleHide, fetchJobs]);

    {/*<input className="ml-3" onClick={() => toggleToggle(index)} type="checkbox"></input>*/ }
    return (
        <>
            <div className="flex flex-col gap-3 h-screen no-scrollbar overflow-y-auto">
                <div className="border-2 border-amber-900 text-center">
                    <form>
                        <p className="text-amber-900">Search your jobs</p>
                        <input className="w-full py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline"
                            value={query}
                            onChange={(e) => searchJobs(e.target.value)}
                        />
                    </form>
                </div>
                <p>{jobs.length} jobs</p>
                {jobs?.map((job) => (
                    <div key={job.id} className={`flex flex-col border rounded-xl border-current p-4 hover:bg-amber-100 ${clickedJob === job ? 'bg-amber-100' : ''}`}>
                        <div className="flex justify-between">
                            <p className="text-xs overflow-hidden">{job.post_date}</p>
                            <button className="self-center border-2 border-amber-950 text-xs text-black h-5 w-3/12 mr-4"
                                onClick={() => hideJob(job.id)}
                            >
                                Hide
                            </button>
                        </div>
                        <div onClick={() => handleClick(job)}>
                            <div className="flex justify-between">
                                <div className="flex-col">
                                    <p className="overflow-hidden text-xl font-bold text-amber-900 ">{tc(job.title)}</p>
                                    <p className="overflow-hidden text-sm">{job.company}</p>
                                    {job.websites_id === 1 ? <p className="text-sm text-amber-800">{job.position}</p> :
                                        null}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </>
    );
};

export default Jobs;
