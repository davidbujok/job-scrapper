import { useState } from "react";
import Jobs from "./Components/Jobs";
import { Job as JobType } from "./Interfaces";
import JobComponent from "./Components/JobComponent";
import Navbar from "./Components/Navbar";
import CreateDocs from "./Components/CreateDocsComponent";

function App() {
    const [job, setJob] = useState<JobType | null>(null);
    const [docsPage, setDocsPage] = useState<boolean>(false);
    const [jobs, setJobs] = useState<Array<JobType>>([]);

    return (
        <>
            <Navbar setJobs={setJobs} jobs={jobs} setDocsPage={setDocsPage}/>
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
