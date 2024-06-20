import { Dispatch, SetStateAction } from "react";
import { Job as JobType } from "../Interfaces"

interface JobComponentProps {
    job: JobType;
    setDocsPage: Dispatch<SetStateAction<boolean>>;
}

export default function JobComponent({ job, setDocsPage }: JobComponentProps) {

    return (
        <>
            <div className="flex flex-col bg-zinc-100 gap-3 p-20">
                <div className="flex">
                    <div className="w-10/12">
                        <h1 className="text-4xl font-medium">{job.position}</h1>
                        <h2 className="text-2xl italic font-medium">{job.title}</h2>
                    </div>
                    <button className="w-44 bg-amber-800 h-10 rounded self-center text-white font-bold"
                        onClick={() => setDocsPage(true)}
                    >
                        Create Docs
                    </button>
                </div>
                <a className="font-mono text-blue-900" href={job.url}>Link to job webpage</a>
                <h3 className="text-2xl font-semibold">{job.location}</h3>
                <div className="mt-5 flex">
                    <div className="w-1/12 bg-amber-900 mr-5"></div>
                    <p className="text-2xl">{job.about}</p>
                </div>
            </div>

        </>
    )
}
