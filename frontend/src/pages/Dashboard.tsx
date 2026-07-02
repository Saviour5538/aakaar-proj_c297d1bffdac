import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchDocuments, fetchConversations } from '../api/client';
import { Document, Conversation } from '../types';
import { toast } from 'react-toastify';

const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [documentsResponse, conversationsResponse] = await Promise.all([
          fetchDocuments(),
          fetchConversations(),
        ]);
        setDocuments(documentsResponse);
        setConversations(conversationsResponse);
      } catch (err) {
        setError('Failed to fetch data. Please try again.');
        toast.error('Failed to fetch data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleUploadClick = () => {
    navigate('/upload');
  };

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      {loading ? (
        <div className="text-center text-gray-500">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-500">{error}</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white shadow rounded-lg p-4">
              <h2 className="text-lg font-semibold">Documents</h2>
              <p className="text-2xl font-bold">{documents.length}</p>
            </div>
            <div className="bg-white shadow rounded-lg p-4">
              <h2 className="text-lg font-semibold">Conversations</h2>
              <p className="text-2xl font-bold">{conversations.length}</p>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">Recent Documents</h2>
            {documents.length > 0 ? (
              <ul className="bg-white shadow rounded-lg divide-y">
                {documents.slice(0, 5).map((doc) => (
                  <li key={doc.id} className="p-4">
                    {doc.name}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No documents available.</p>
            )}
          </div>

          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">Recent Conversations</h2>
            {conversations.length > 0 ? (
              <ul className="bg-white shadow rounded-lg divide-y">
                {conversations.slice(0, 5).map((conv) => (
                  <li key={conv.id} className="p-4">
                    {conv.title}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No conversations available.</p>
            )}
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleUploadClick}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            >
              Upload Document
            </button>
            <button
              onClick={handleChatClick}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
            >
              Start Chat
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;