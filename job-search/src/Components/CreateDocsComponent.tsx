import { useState } from "react";
import { Job as JobType } from "../Interfaces"
import OpenAI from 'openai'
import { prompt_personal_statement } from "../assets/cv.tsx"

interface JobComponentProps {
    job: JobType | null;
    //const [job, setJob] = useState<JobType | null>(null);
}
interface OpenAIResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    choices: [];
}


export default function CreateDocs({ job }: JobComponentProps) {
    const [responseData, setResponseData] = useState<OpenAIResponse | null>(null);
    const openai = new OpenAI({
        apiKey: import.meta.env.VITE_OPENAI_API_KEY,
        dangerouslyAllowBrowser: true
    });
    let prompt = prompt_personal_statement(job)
    console.log(prompt)

    async function activateDocsGeneration() {
        try {
            const completion = await openai.chat.completions.create({
                messages: [{
                    role: "user",
                    content: prompt
                }],
                model: "gpt-3.5-turbo",
            });
            return completion; // Returning full completion to handle in the calling method
        } catch (error) {
            console.error("Error while fetching data from OpenAI:", error);
            return null;
        }
    }

    const handleClick = async () => {
        console.log("Generating docs...");
        const completion = await activateDocsGeneration();
        if (completion) {
            setResponseData(completion); // Correctly set response data
        } else {
            //setResponseData("Failed to generate document"); // Error fallback handling
            setResponseData(null); // Error fallback handling
        }
    };
    //<p key={choice.id}>{choice.message.content}</p>
    //{responseData ?
    //    <p>{responseData.choices[0].message.content}</p> : // Directly render response data
    //    <p>No Document Generated</p> // Fallback content
    //}
    return (
        <>

            {
                job ?
                    <>
                        <h1>{job.position}</h1>
                        <h2>{job.title}</h2>
                        <h3>{job.company}</h3>
                    </>
                    : <p>nioh</p>
            }
            <button className="h-10 w-40 bg-red-800 rounded" onClick={handleClick}>
                Generate Docs
            </button>
            {responseData && responseData.choices.length > 0 ?
                responseData.choices.map(choice => (
                    <p>{choice.message.content}</p>
                )) :
                <p>No Document Generated</p>
            }
        </>
    );
}

