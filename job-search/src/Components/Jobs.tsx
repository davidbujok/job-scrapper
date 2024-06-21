import { Dispatch, useCallback, useEffect, useState } from "react";
import { Job as JobType } from "../Interfaces";

interface JobsProps {
    setJob: Dispatch<React.SetStateAction<JobType | null>>;
    setJobs: Dispatch<React.SetStateAction<JobType[]>>;
    jobs: JobType[];
}

const Jobs = ({ setJob, jobs, setJobs }: JobsProps) => {
    const [toggleHide, setToggleHide] = useState<boolean>(false)
    //async function fetchJobs() {
    //    const response = await fetch("http://127.0.0.1:5000/jobs");
    //    const jobs = await response.json();
    //    setJobs(jobs);
    //}
    const fetchJobs = useCallback(async () => {
        const response = await fetch("http://127.0.0.1:5000/jobs");
        const jobsData = await response.json();
        setJobs(jobsData);
    }, [setJobs]);


    const hideJob = async (jobId: number) => {
        await fetch(`http://127.0.0.1:5000/hide_job/${jobId}`);
        setToggleHide(prev => !prev);  // Toggle the value to ensure state change
    }

    //async function hideJob(jobId: number) {
    //    await fetch(`http://127.0.0.1:5000/hide_job/${jobId}`);
    //    setToggleHide(true)
    //    //const junior_jobs = await response.json();
    //    //setJobs(junior_jobs);
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
    }, [toggleHide, fetchJobs]);

    {/*<input className="ml-3" onClick={() => toggleToggle(index)} type="checkbox"></input>*/ }
    return (
        <>
            <div className="bg-stone-200 border rounded-s p-10 flex flex-col gap-3">
                {jobs?.map((job) => (
                    <div key={job.id} className="flex border rounded-xl border-current p-4 hover:bg-amber-100">
                        <div className="self-center bg-blue-500 rounded text-center text-white h-6 w-2/12 mr-4"
                            onClick={() => hideJob(job.id)}
                        >
                            Hide
                        </div>
                        <div onClick={() => setJob(job)} className="mb-2 text-xl w-10/12">
                            <div className="flex justify-between">
                                <div className="flex-col w-10/12">
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
