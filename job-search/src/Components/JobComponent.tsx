import { Dispatch, SetStateAction } from "react";
import { Job as JobType } from "../Interfaces"

interface JobComponentProps {
    job: JobType;
    setDocsPage: Dispatch<SetStateAction<boolean>>;
}

export default function JobComponent({ job, setDocsPage }: JobComponentProps) {

    return (
        <>
            <div className="flex flex-col bg-zinc-100 gap-2 p-5">
                <div className="flex">
                    <div className="w-10/12">
                        <h1 className="text-xl font-medium">{job.position}</h1>
                    </div>
                </div>
                <a className="font-mono text-blue-900" href={job.url}>Link to job webpage</a>
                {
                    job.websites_id === 1 ? <h1 className="font-mono text-blue-900">from LinkedIN</h1> :
                        <h1 className="font-mono text-blue-900">Indeed</h1>
                }
                <h3 className="font-semibold">{job.location}</h3>
                <button className="w-44 bg-amber-800 h-8 rounded text-white font-bold"
                    onClick={() => setDocsPage(true)}
                >
                    Create Docs
                </button>
                <div className="mt-5 flex">
                    <div className="w-1/12 bg-amber-900 mr-5"></div>
                    <p className="text-xl">{job.about}</p>
                </div>
            </div>

        </>
    )
}
