import { useEffect, useState } from "react";
import Jobs from "./Components/Jobs";
import { Job as JobType, User as UserType } from "./Interfaces";
import JobComponent from "./Components/JobComponent";
import Navbar from "./Components/Navbar";
import CreateDocs from "./Components/CreateDocsComponent";

function App() {
    const [job, setJob] = useState<JobType | null>(null);
    const [docsPage, setDocsPage] = useState<boolean>(false);
    const [jobs, setJobs] = useState<Array<JobType>>([]);
    const [userJobs, setUserJobs] = useState<UserType | null>(null)

    const url = window.location.href;

    const pathParts = url.split('/');
    const userId = pathParts[pathParts.length - 1]; // Gets the last part of the URL

    const fetchUserJobs = async (userId: string) => {
        const response = await fetch(`http://127.0.0.1:5000/jobs/user/${userId}`);
        const userJobsData = await response.json();
        console.log(userJobsData)
        setUserJobs(userJobsData);
    };
    useEffect(() => { fetchUserJobs(userId) }, [])

    return (
        <>
            <Navbar userJobs={userJobs} setJobs={setJobs} setUserJobs={setUserJobs} jobs={jobs} setDocsPage={setDocsPage}/>
            {docsPage ?
                <CreateDocs job={job}></CreateDocs>
                :
                <div className="flex ml-11 gap-14">
                    <div className="w-2/5">
                        <Jobs setJob={setJob} jobs={jobs} setJobs={setJobs} ></Jobs>
                    </div>
                    <div className="w-3/5 mr-11">{job && <JobComponent job={job} setDocsPage={setDocsPage} />}</div>
                </div>
            }
        </>
    );
}

export default App;
