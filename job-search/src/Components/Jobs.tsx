import { Dispatch, useEffect } from "react";
import { Job as JobType } from "../Interfaces";

interface JobsProps {
    setJob: Dispatch<React.SetStateAction<JobType | null>>;
    setJobs: Dispatch<React.SetStateAction<JobType[]>>;
    jobs: JobType[];
}

const Jobs = ({ setJob, jobs, setJobs }: JobsProps) => {
    async function fetchJobs() {
        const response = await fetch("http://127.0.0.1:5000/jobs");
        const jobs = await response.json();
        setJobs(jobs);
    }

    //async function fetchJuniorJobs() {
    //    const response = await fetch("http://127.0.0.1:5000/junior_jobs");
    //    const junior_jobs = await response.json();
    //    setJobs(junior_jobs);
    //}

    //const toggleToggle = (index: number) => {
    //    const jobsCopy = [...jobs];
    //    const job = jobsCopy[index];
    //    console.log(job.apply_status);
    //    job.apply_status = job.apply_status ? false : true;
    //    console.log(job.apply_status);
    //    jobsCopy[index] = job;
    //    setJobs(jobsCopy);
    //};

    useEffect(() => {
        fetchJobs();
    }, []);

    {/*<input className="ml-3" onClick={() => toggleToggle(index)} type="checkbox"></input>*/ }
    return (
        <>
            <div className="bg-stone-200  border rounded-s p-10 flex flex-col gap-3">
                {jobs?.map((job) => (
                    <div key={job.id} className="border rounded-xl border-current p-4 hover:bg-amber-100">
                        <div onClick={() => setJob(job)} className="mb-2 text-xl ">
                            <div className="flex justify-between">
                                <div className="flex-col">
                                    <p className="overflow-hidden text-3xl font-bold text-amber-900 ">{job.title}</p>
                                    <p className="overflow-hidden text-2xl">{job.company}</p>
                                </div>
                                <p className="overflow-hidden">{job.post_date}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </>
    );
};

export default Jobs;
