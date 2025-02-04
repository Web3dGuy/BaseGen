// fileTypeFilters.js
export const folderFilters = {
  "Music": {
    extensions: [".mp3", ".m4a", ".flac", ".wav", ".aac", ".ogg", ".wma"],
    description: "Audio files (mp3, m4a, flac, etc.)"
  },
  "Movies": {
    extensions: [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".m4v", ".webm"],
    description: "Video files (mp4, mkv, avi, etc.)"
  },
  "TV Shows": {
    extensions: [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".m4v", ".webm"],
    description: "Video files (mp4, mkv, avi, etc.)"
  },
  "Pictures": {
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".heic"],
    description: "Image files (jpg, png, gif, etc.)"
  },
  "Audio Books": {
    extensions: [".mp3", ".m4a", ".m4b", ".aac", ".ogg", ".wma"],
    description: "Audio files (mp3, m4a, m4b, etc.)"
  }
};

export function getFilterForFolder(folderName) {
  // Case-insensitive matching for folder names
  const normalizedName = folderName.toLowerCase();
  const match = Object.entries(folderFilters).find(([key]) => 
    key.toLowerCase() === normalizedName
  );
  
  return match ? match[1] : null;
}

export function isFileAllowed(filename, folderName) {
  const filter = getFilterForFolder(folderName);
  if (!filter) return true; // If no filter defined, allow all files
  
  const ext = filename.toLowerCase().slice(filename.lastIndexOf('.'));
  return filter.extensions.includes(ext);
}

export function getAcceptString(folderName) {
  const filter = getFilterForFolder(folderName);
  if (!filter) return '';
  
  return filter.extensions.join(',');
}

export function getFolderDescription(folderName) {
  const filter = getFilterForFolder(folderName);
  return filter ? filter.description : "All files";
}
