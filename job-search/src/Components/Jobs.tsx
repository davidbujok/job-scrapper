import { Dispatch, useCallback, useEffect, useState } from "react";
import { Job as JobType } from "../Interfaces";

interface JobsProps {
    setJob: Dispatch<React.SetStateAction<JobType | null>>;
    setJobs: Dispatch<React.SetStateAction<JobType[]>>;
    jobs: JobType[];
}

const Jobs = ({ setJob, jobs, setJobs }: JobsProps) => {
    const [toggleHide, setToggleHide] = useState<boolean>(false)

    const fetchJobs = useCallback(async () => {
        const response = await fetch("http://127.0.0.1:5000/jobs");
        const jobsData = await response.json();
        setJobs(jobsData);
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
            <div className="flex flex-col gap-3">
                {jobs?.map((job) => (
                    <div key={job.id} className="flex flex-col border rounded-xl border-current p-4 hover:bg-amber-100">
                        <div className="flex justify-between">
                            <p className="text-xs overflow-hidden">{job.post_date}</p>
                            <button className="self-center border-2 border-amber-950 text-xs text-black h-5 w-3/12 mr-4"
                                onClick={() => hideJob(job.id)}
                            >
                                Hide
                            </button>
                        </div>
                        <div onClick={() => setJob(job)} className="mb-2 text-xl">
                            <div className="flex justify-between">
                                <div className="flex-col">
                                    <p className="overflow-hidden text-1xl font-bold text-amber-900 ">{job.title}</p>
                                    <p className="overflow-hidden text-sm">{job.company}</p>
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
