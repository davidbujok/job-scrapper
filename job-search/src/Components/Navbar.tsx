import { Dispatch, SetStateAction, useState } from "react";
import { Job as JobType, User as UserType } from "../Interfaces"
import ScrapeJobs from "./ScrapeJobs";

interface JobProps {
    setJobs: Dispatch<React.SetStateAction<JobType[]>>
    jobs: JobType[]
    userJobs: UserType | null
    setDocsPage: Dispatch<SetStateAction<boolean>>;
    setUserJobs: Dispatch<SetStateAction<UserType | null>>;
}

export default function Navbar({ userJobs, setUserJobs, setDocsPage }: JobProps) {

    const [scrapePage, setScrapePage] = useState<boolean>(false)

    return (
        <>
            {scrapePage ? <ScrapeJobs userJobs={userJobs} setUserJobs={setUserJobs} setScrapePage={setScrapePage} /> :
                <div className="flex bg-amber-800 justify-between mb-5 pt-2 h-20">
                    <div className="flex gap-10 ml-10">
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
